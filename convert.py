#!/usr/bin/env python

# Copyright 2012 Philipp Klaus
# Part of https://github.com/vLj2/wikidot-to-markdown

# Later editing: 2017 Zoltan Schmidt

from wikidot import WikidotToMarkdown ## most important here

import sys ## for sys.exit()
import os ## for os.makedirs()
import optparse ## for optparse.OptionParser()
# import markdown ## for markdown.markdown()
import codecs ## for codecs.open()

DEFAULT_OUTPUT_DIR = "output"

class ConversionController(object):
    def __init__(self, options):
        self.__input_wiki_file = options.filename
        self.__input_directory = options.input_dir
        self.__output_directory = options.output_dir
        self.__converter = WikidotToMarkdown()

    def __prepare_output_dir(self):
        try:
            os.makedirs(self.__output_directory)
        except OSError as ex:
            print("Could not create output folder "+self.__output_directory+".")
            if ex.errno == os.errno.EEXIST: print("It already exists.")
            else: print "Error %i: %s" % (ex.errno, str(ex)); sys.exit(1)


    def convert(self):
        self.__prepare_output_dir()

        def convertonefile(self, thispath):
            f = codecs.open(thispath, encoding='utf-8')
            text = f.read()

            # write the complete files to the output directory:
            complete_text = self.__converter.convert(text)

            name = os.path.basename(os.path.splitext(thispath)[0])
            self.write_unicode_file("%s/%s" % (self.__output_directory, name+'.md'),complete_text)


        #if one file
        if self.__input_directory == None:
            convertonefile(self, self.__input_wiki_file)

        #if an entire folder
        else:
            for filename in os.listdir(self.__input_directory):
                if filename.endswith(".txt"):
                    #print(os.path.join(self.__input_directory, filename))
                    convertonefile(self, os.path.join(self.__input_directory, filename))
                    continue
                else:
                    continue





    def write_unicode_file(self, path_to_file, content):
        try:
            out_file = codecs.open(path_to_file,encoding='utf-8', mode='w')
            out_file.write(content)
        except:
            print "Error on writing to file %s." % path_to_file


def main():
    """ Main function called to start the conversion."""
    p = optparse.OptionParser(version="%prog 1.0")

    # set possible CLI options
    p.add_option('--input-file', '-f', metavar="INPUT_FILE", help="Read from INPUT_FILE.", dest="filename")
    p.add_option('--input-dir', '-d', metavar="INPUT_DIR", help="Read all text from INPUT_DIR.", dest="input_dir")
    p.add_option('--output-dir', '-o', metavar="OUTPUT_DIRECTORY", help="Save the converted files to the OUTPUT_DIRECTORY.", dest="output_dir")

    # parse our CLI options
    options, arguments = p.parse_args()
    if options.filename == None and options.input_dir == None:
        p.error("No input set. Have a look at the parameters using the option -h.")
        sys.exit(1)

    if options.output_dir == None:
        options.output_dir = raw_input('Please enter an output directory for the converted documents [%s]: ' % DEFAULT_OUTPUT_DIR)
        if options.output_dir == "": options.output_dir = DEFAULT_OUTPUT_DIR

    converter = ConversionController(options)
    converter.convert()

if __name__ == '__main__':
    main()
