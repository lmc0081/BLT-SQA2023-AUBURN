from io import TextIOWrapper
import json
import graphtaint


def fuzzGetYamlFiles(val1, outputFile: TextIOWrapper):
    outputFile.write("Fuzzing getYAMLFiles\n")
    try:
        res = graphtaint.getYAMLFiles(val1)
        return res
    except Exception as error:
        outputFile.write("Input: " + str(val1) + " --> Error: " + str(error) + "\n")
    outputFile.write("\n")


def fuzzGetValidTaints(val1, outputFile: TextIOWrapper):
    outputFile.write("Fuzzing getValidTaints\n")
    try:
        res = graphtaint.getValidTaints(val1)
        return res
    except Exception as error:
        outputFile.write("Input: " + str(val1) + " --> Error: " + str(error) + "\n")
    outputFile.write("\n")


def fuzzMineSecretGraph(val1, val2, val3, outputFile: TextIOWrapper):
    outputFile.write("Fuzzing mineSecretGraph\n")
    try:
        res = graphtaint.mineSecretGraph(val1, val2, val3)
        return res
    except Exception as error:
        outputFile.write(
            "Input: "
            + str(val1)
            + ", "
            + str(val2)
            + ", "
            + str(val3)
            + " --> Error: "
            + str(error)
            + "\n"
        )
    outputFile.write("\n")


def fuzzGetMatchingTemplates(val1, val2, outputFile: TextIOWrapper):
    outputFile.write("Fuzzing getMatchingTemplates\n")
    try:
        res = graphtaint.getMatchingTemplates(val1, val2)
        return res
    except Exception as error:
        outputFile.write(
            "Input: "
            + str(val1)
            + ", "
            + str(val2)
            + " --> Error: "
            + str(error)
            + "\n"
        )
    outputFile.write("\n")


def fuzzGetSHFiles(val1, outputFile: TextIOWrapper):
    outputFile.write("Fuzzing getSHFiles\n")
    try:
        res = graphtaint.getSHFiles(val1)
        return res
    except Exception as error:
        outputFile.write("Input: " + str(val1) + " --> Error: " + str(error) + "\n")
    outputFile.write("\n")


def fuzzer():
    blnsFile = open("blns.json", "r")
    data = json.load(blnsFile)

    outputFile = open("fuzzedErrors.txt", "w")

    for i in range(0, len(data)):
        fuzzGetYamlFiles(data[i], outputFile)
        fuzzGetValidTaints(data[i], outputFile)
        fuzzMineSecretGraph(data[i], data[i], data[i], outputFile)
        fuzzGetMatchingTemplates(data[i], data[i], outputFile)
        fuzzGetSHFiles(data[i], outputFile)
    outputFile.close()
    blnsFile.close()


if __name__ == "__main__":
    fuzzer()
