# 📜 Spreadsheet to JSON converter

**This is a python scripts for retrieving Google spreadsheet content and convert data into JSON files**

![Language](https://img.shields.io/github/languages/top/cjdriod/Spreadsheet-to-Json?style=flat-square)
![Size](https://img.shields.io/github/repo-size/cjdriod/Spreadsheet-to-Json?style=flat-square)

## 🔨 Installation
### Prerequisites
* **Python** - Version 3.7 or [greater](https://www.python.org/downloads/)
* **The [pip](https://pypi.org/project/pip/) package management tool**
* **Google Account**

### Basic Usage
Install virtualenv via pip:
```
$ pip install virtualenv
```
Test your installation:
```
$ virtualenv --version
```
<br>

1. Create a virtual environment for a project:
```
$ cd project_folder
$ virtualenv venv
```

2. To begin using the virtual environment, it needs to be activated:
```
$ source venv/bin/activate

window platform:
venv\Scripts\activate
```

3. Install dependencies
```
$ pip install -r requirements.txt
```

4. Create `.env` file (you can refer `.env.example` file or [environment configuration below](#%EF%B8%8F-config-environment-variables)
<br>
   
## ⚙️ Config Environment Variables
> **LOCALHOST_PORT**  
> `Type: Int | Default: 0`  
> 
> Google OAuth 2.0 service authentication page hosting port number.

> **EMPTY_DATA_FILTER**  
> `Type: Bool | Default: False | Options: (True || False)`  
> 
> Google OAuth 2.0 service authentication page hosting port number.

> **SOURCE_1_NAMESPACE**  
> `Type: String | Required: True`
> 
> An identifier for the current task, also the output folder name in your output directory.
  
> **SOURCE_1_CREDENTIAL_FILE_NAME**  
> `Type: String | Required: True`
> 
> The credential file name that provided by Google Cloud when enabling the api service.  
> E.g. `credentail.json -> SOURCE_1_CREDENTIAL_FILE_NAME = credential`
> 
> ***Note: Exclude file extension name!***  
>
> Refers [Google Spreadsheet documentation](https://developers.google.com/sheets/api/quickstart/python) steps to obtain the credential file

> **SOURCE_1_ACCESS_TOKEN_FILE_NAME**  
> `Type: String | Required: True`
> 
> File that store your session access token  
> 
> Note: The file name must be **UNIQUE**

> **SOURCE_1_SPREADSHEET_ID**  
> `Type: String | Required: True`
> 
> Your Google Spreadsheet sheet ID number
> ```
> E.g.
> https://docs.google.com/spreadsheets/d/1FhgZIa07IStNoei-Yt61JjJeGh-EIqqMxm6vLE85_wc/edit#gid=0
> SOURCE_1_SPREADSHEET_ID = 1FhgZIa07IStNoei-Yt61JjJeGh-EIqqMxm6vLE85_wc
> ```

> **SOURCE_1_SHEET_NAME**  
> `Type: String | Required: True`
> 
> The Google Spreadsheet sheet name that you want to get data from  
> E.g. `SOURCE_1_SHEET_NAME = Demo`
> >![spreadsheet sheet name screenshot](public/image/spreadsheet_sheet_name_screenshot.PNG)

>**Note: Add ons**  
> This script reserve another sets of environment variable to perform 2 jobs in 1 script run.   
> Below are the environment variables:
> - SOURCE_2_NAMESPACE
> - SOURCE_2_SHEET_NAME
> - SOURCE_2_SPREADSHEET_ID
> - SOURCE_2_CREDENTIAL_FILE_NAME
> - SOURCE_2_ACCESS_TOKEN_FILE_NAME  
> 
> Note: You can add more variables and modify the scripts based on your needs

## 🎄 Additional Configuration
Additional configuration files settings 

_Ps: These are not environment variables_  
**Note: Both configuration files(JSON) mention below must be stored in `/data` directory**

> **artifact-export-lookup-table.json**   
> This file teaches the script how to export the result you get from the spreadsheet
> ``` 
> {
>   "english": "locale-en", // "column_name": "export_file_name_ONLY_without_file_extention"
>   "chinese": "locale-zh"
> }
> ```

> **preset-directory.json**  
> Render pre-defined output directory profile selection interface(CLI)
> ``` 
> {
>   "directories": [
>       {
>           "index": "1", <------------------------------ The selection ID,
>           "name": "Profile 1", <----------------------- The Selection display name
>           "path": "D:\\SpreadsheetExport\\Profile1" <-- Output base directory absolute file path
>       },
>       {
>           "index": "2",
>           "name": "Profile 2",
>           "path": "D:\\SpreadsheetExport\\Profile2"
>       }
>   ]
> }
> ```

> **Environment file support**  
> This project uses [python-decouple 3.4](https://pypi.org/project/python-decouple/) for environment variable control  
> Supported environment variable file:  
> 1. `ini` file
> 2. `.env` file (author selection)

## 🩹 Limitation
- Only design to export JSON file
- Only design to export entire spreadsheet data, unable to performs specific range data capture or formatting which supported by Google Spreadsheet API.

Happy Coding~ you can modify the script based on your needs 🏀

## ⚔️ Contributing
Pull requests are welcome.

### Commit message format
We are following [Semantic Commit Messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716) approach   
Format: `<type>: <subject>`
```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```
- feat: (new feature for the user, not a new feature for build script)
- fix: (bug fix for the user, not a fix to a build script)
- docs: (changes to the documentation)
- style: (formatting, spacing, etc; no production code change)
- refactor: (refactoring production code, eg. renaming a variable)
- test: (adding missing tests, refactoring tests; no production code change)
- chore: (updating grunt tasks etc; no production code change)

### Pull Request Title
The title of the pull request are required to follow commit message format [above](#commit-message-format)  
PR description can be added for more context references

### Linting
Please use linting tools below to ensure your pull request compliance with [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard 
- SonarLint
- Pylint

Note: The maintainer reserved the rights to NOT merge the PR, if failed to follow any requirement listed above

## 🎊 Authors and acknowledgment
- cjdriod [ [jacklim.cj@gmail.com](mailto:jacklim.cj@gmail.com) ]

## 📝 License
![License](https://img.shields.io/github/license/cjdriod/Spreadsheet-to-Json?style=for-the-badge)
