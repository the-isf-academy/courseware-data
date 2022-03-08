#!/bin/bash
export PATH=$PATH:~/Library/Python/3.8/bin >> ~/.zshrc 
source ~/.zshrc

pip3 install notebook
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main && jupyter nbextension enable collapsible_headings/main && jupyter nbextension enable hide_input/main && jupyter nbextension enable varInspector/main && jupyter nbextension enable hinterland/hinterland && jupyter nbextension enable python-markdown/main && jupyter nbextension enable spellchecker/main && jupyter nbextension enable exercise2/main
