# To add the module path into python site-packages with ***.pth*** file
1. Add the whole QM_opt module path into the python site-packages folder. 
2. Check the root to the QM_opt folder use: 
    `import os`  
    `print(os.getcwd())`
    , print it in a py in that folder.
3. Get the python site-packages absolute path use:
    `import sys`
    `print(sys.path)`
    , you can also print it in the same file as the previous step.
4. Open a terminal and active the virtual environment which will run the py file. Type in:
    `cd {site-packages path}`
    fill the actual path into the { }.
5. Add the path use:
    `sudo echo "{QM_opt module path}" > {arbitrary name}.pth`
    fill the actual path and a name into the { }.
6. Check it works or not.
    