#!/usr/bin/env python3


from enum import Enum
import getopt, os, shutil, sys


cleanerName = os.path.basename(os.path.splitext(__file__)[0])
versions = ["16.0", "16.1"]


def printError(error, usageFunc, mustExit=False, addInfo=None, addInfos=[]):
	sys.stderr.write("Error: {}{}\n".format(error.value[0], ": {}".format(addInfo) if addInfo is not None else ""))
	for i in addInfos:
		levelPrint(i[1], i[0], printFunction=sys.stderr.write)
		sys.stderr.write("\n")

	if error.value[1]:
		sys.stderr.write("\n")
		usageFunc(True)
	if mustExit:
		exit(1)


def printWarning(warning, addInfo=None, addInfos=[]):
	sys.stderr.write("Warning: {}{}\n".format(warning.value, ": {}".format(addInfo) if addInfo is not None else ""))
	for i in addInfos:
		levelPrint(i[1], i[0], printFunction=sys.stderr.write)
		sys.stderr.write("\n")


class Errors(Enum):
	NO_ERRORS = ("No errors", False)
	GENERAL_ERROR = ("An unhandled general error occurred. Additional info may follow", False)
	EXTERNAL_ERROR = ("An error happened outside of this tool. Additional info may follow", False)
	GETOPT_ERROR = ("Error parsing arguments", True)
	MISSING_ARGUMENT = ("Missing argument for this command", True)
	INVALID_VERSION = ("Invalid Quartus version", True)
	NOT_A_PROJECT = ("Specified folder does not have a valid Quartus project hierarchy or project name is incorrect", False)


class Warnings(Enum):
	USING_DEFAULT_VALUE = "Using default value"


def printUsage(printToError=False):
	usageStr = (
		'AOCLCleaner: a cleaner for OpenCL Quartus II projects\n'
		'\n'
		'Usage: {0} ARGS... PATH\n'
		'Where ARGS can be:\n'
		'	-d, --dry-run		  : don\'t modify anything, just print what would be kept and deleted\n'
		'	-v, --version=VERSION  : specify Quartus version of the project\n'
		'	-p, --project-name=NAME: specify the project name (default is top)\n'
		'	-h, --help			 : show this message\n'
		'Where PATH is the path to the Quartus project folder\n'
		'\n'
		'Supported Quartus versions:\n'
		'	{1}'.format(cleanerName, ", ".join(map(str, versions)))
	)

	if printToError:
		sys.stderr.write("{}\n".format(usageStr))
	else:
		print(usageStr)


def getTotalFolderSize(path="."):
	totalSize = 0
	for dirPath, dirNames, fileNames in os.walk(path):
		for f in fileNames:
			fp = os.path.join(dirPath, f)
			totalSize += os.path.getsize(fp)

	unitList = ["B", "kB", "MB", "GB"]
	unitBinList = ["B", "KiB", "MiB", "GiB"]
	unit = 0
	totalBinSize = totalSize
	while totalSize >= 1000:
		totalSize /= 1000
		totalBinSize /= 1024
		unit += 1

	return "{:.2f} {} ({:.2f} {})".format(totalSize, unitList[unit], totalBinSize, unitBinList[unit])


if "__main__" == __name__:
	opts = []
	args = []
	dryRun = False
	version = "16.1"
	versionSet = False
	projectName = "top"
	projectNameSet = False

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hdp:v:", ["help", "dry-run", "project-name=", "version="])
	except getopt.GetoptError as err:
		printError(Errors.GETOPT_ERROR, printUsage, True, str(err))

	for o, a in opts:
		if o in ("-d", "--dry-run"):
			dryRun = True
		elif o in ("-v", "--version"):
			version = a
			versionSet = True
		elif o in ("-p", "--project-name"):
			projectName = a
			projectNameSet = True
		else:
			printUsage()
			exit(0)

	if 0 == len(args):
		printError(Errors.MISSING_ARGUMENT, printUsage, True, "PATH")
	if version not in versions:
		printError(Errors.INVALID_VERSION, printUsage, True, version)
	if not versionSet:
		printWarning(Warnings.USING_DEFAULT_VALUE, "-v/--version={}".format(version))
	if not projectNameSet:
		printWarning(Warnings.USING_DEFAULT_VALUE, "-p/--project-name={}".format(projectName))

	if dryRun:
		print("> Running in dry-run mode")

	if not os.path.isfile(os.path.join(args[0], "{}.qpf".format(projectName))):
		printError(Errors.NOT_A_PROJECT, None, True)

	print("> Current project size: {}".format(getTotalFolderSize(args[0])))

	if "16.0" == version:
		# TODO
		pass
	elif "16.1" == version:
		toRemoveFolders = [
			"db",
			"incremental_db",
			"persona",
			"system"
		]
		toRemoveFiles = [
		]
		toRemoveByExtension = [
			".sof",
			".rbf",
			".aocx",
			".bin"
		]

		try:
			for p in os.listdir(args[0]):
				fullPath = os.path.join(args[0], p)
				if p in toRemoveFolders:
					print("> Removing {} folder...".format(p))
					if not dryRun:
						shutil.rmtree(fullPath)
				elif p in toRemoveFiles:
					print("> Removing {} file...".format(p))
					if not dryRun:
						os.remove(fullPath)
				elif os.path.splitext(p)[1] in toRemoveByExtension:
					print("> Removing {} file...".format(p))
					if not dryRun:
						os.remove(fullPath)
		except Exception as err:
			printError(Errors.EXTERNAL_ERROR, None, True, str(err))


	print("> Final project size: {}".format(getTotalFolderSize(args[0])))
