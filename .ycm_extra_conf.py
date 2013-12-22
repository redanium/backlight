import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-x',
'c++',
'-Wall',
'-Wextra',
'-fPIE',
'-D_REENTRANT',
'-std=c++1y',
'-stdlib=libc++',
'-ftemplate-depth=8192',
'-fconstexpr-depth=8192',
'-lcxxrt',
'-ldl',
'-isystem', '/usr/include/c++/v1',
'-isystem', '/usr/local/include',
'-isystem', '/usr/include/x86_64-linux-gnu',
'-isystem', '/usr/include',
'-I', '/usr/local/src/yeppp/1.0.0/library/headers',
'-I', '/opt/qt/5.2.0/linux/mkspecs/linux-clang',
'-I', '/opt/qt/5.2.0/linux/include',
'-I', '/opt/qt/5.2.0/linux/include/QtCLucene',
'-I', '/opt/qt/5.2.0/linux/include/QtConcurrent',
'-I', '/opt/qt/5.2.0/linux/include/QtCore',
'-I', '/opt/qt/5.2.0/linux/include/QtDBus',
'-I', '/opt/qt/5.2.0/linux/include/QtDeclarative',
'-I', '/opt/qt/5.2.0/linux/include/QtDesigner',
'-I', '/opt/qt/5.2.0/linux/include/QtDesignerComponents',
'-I', '/opt/qt/5.2.0/linux/include/QtGui',
'-I', '/opt/qt/5.2.0/linux/include/QtHelp',
'-I', '/opt/qt/5.2.0/linux/include/QtMultimedia',
'-I', '/opt/qt/5.2.0/linux/include/QtMultimediaQuick_p',
'-I', '/opt/qt/5.2.0/linux/include/QtMultimediaWidgets',
'-I', '/opt/qt/5.2.0/linux/include/QtNetwork',
'-I', '/opt/qt/5.2.0/linux/include/QtOpenGL',
'-I', '/opt/qt/5.2.0/linux/include/QtOpenGLExtensions',
'-I', '/opt/qt/5.2.0/linux/include/QtPlatformSupport',
'-I', '/opt/qt/5.2.0/linux/include/QtPrintSupport',
'-I', '/opt/qt/5.2.0/linux/include/QtQml',
'-I', '/opt/qt/5.2.0/linux/include/QtQuick',
'-I', '/opt/qt/5.2.0/linux/include/QtQuickParticles',
'-I', '/opt/qt/5.2.0/linux/include/QtQuickTest',
'-I', '/opt/qt/5.2.0/linux/include/QtScript',
'-I', '/opt/qt/5.2.0/linux/include/QtScriptTools',
'-I', '/opt/qt/5.2.0/linux/include/QtSensors',
'-I', '/opt/qt/5.2.0/linux/include/QtSerialPort',
'-I', '/opt/qt/5.2.0/linux/include/QtSql',
'-I', '/opt/qt/5.2.0/linux/include/QtSvg',
'-I', '/opt/qt/5.2.0/linux/include/QtTest',
'-I', '/opt/qt/5.2.0/linux/include/QtUiTools',
'-I', '/opt/qt/5.2.0/linux/include/QtWebKit',
'-I', '/opt/qt/5.2.0/linux/include/QtWebKitWidgets',
'-I', '/opt/qt/5.2.0/linux/include/QtWidgets',
'-I', '/opt/qt/5.2.0/linux/include/QtX11Extras',
'-I', '/opt/qt/5.2.0/linux/include/QtXml',
'-I', '/opt/qt/5.2.0/linux/include/QtXmlPatterns',

'-I', 'qt-solutions/qtsingleapplication/src',
]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


def FlagsForFile( filename, **kwargs ):
  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )

    # NOTE: This is just for YouCompleteMe; it's highly likely that your project
    # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
    # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
    try:
      final_flags.remove( '-stdlib=libc++' )
    except ValueError:
      pass
  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
