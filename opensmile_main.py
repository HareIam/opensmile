import glob
import os
import wave

from split_silence import split_on_silence_with_pydub


# Function for converting arff list to csv list
def ArfftoCsv(content):

    data = False
    header = ""
    newContent = []
    for line in content:
        if not data:
            if "@attribute" in line:
                attri = line.split()
                columnName = attri[attri.index("@attribute")+1]
                header = header + columnName + ","
            elif "@data" in line:
                data = True
                header = header[:-1]
                #header += '\n'
                newContent.append(header)
        else:
            newContent.append(line)
    return newContent

input_path = './audios/'
temporary_add='./tmp/'
output_path='./results/'
for filename in glob.glob(os.path.join(input_path, '*.wav')):

    # for address in infiles:
    #     os.remove(address)

    arff_files_filename = output_path+os.path.splitext(os.path.basename(filename))[0] + ".arff"

    os.system('@SMILExtract_Release -C config/emobase_live4_batch3'
              '.conf -I '+filename+' -O '+ arff_files_filename)

    # Getting all the arff files from the current directory

    with open(arff_files_filename, "r") as inFile:
        content = inFile.readlines()
        name, ext = os.path.splitext(inFile.name)
        new = ArfftoCsv(content)
        with open(name + ".csv", "w") as outFile:
            outFile.writelines(new)
