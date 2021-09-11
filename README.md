# GTD Templates for Remarkable
Contains templates for GTD writting in tex and utilities for generating svg/png files and uploads templates to remarkable.

DISCLAIMER: Usage of this software is at your own risk and you are responsible for loss of files other damages. Make sure to backup your Remarkable (and the templates) before using this software.

## Examples

|  |  |  |
| --- | --- | --- |
| ![Inbox](examples/inbox.png) | ![Day Planner](examples/day_planner.png) | ![Next Action](examples/next_action.png) 
| ![Project Overview](examples/project_overview.png) | ![Project](examples/project.png) | ![Project Actions](examples/project_actions.png) |

## Installation
The code has been tested using the following setup:

- Ubuntu 18.04
- Python 3.8.0
- pdflatex

Besides from running the code natively on your computer, this project also comes with a slim `Dockerfile` which allows you to create and upload the reMarkable templates on any operating system which [has docker installed](https://docs.docker.com/get-docker/). See usage below.

### LaTeX
A LaTeX compiler for generating the pdf containing the templates. Sevaral LaTeX packages are required, which can be found in the `gtd.tex` file.

### Converting
For converting the pdf to separate png and svg files three linux command line tools are used:
- `pdfseparate` (standard available on Ubuntu)
- `pdf2svg` (standard available on Ubuntu)
- `rsvg-convert` (can be installed using `sudo apt-get install librsvg2-bin`)

### Uploading
The files can be uploaded automatically to the Remarkable over SSH. The python script has two requirements which can be installed by running `python -m pip install -r requirements.txt`.


## Usage
The tex filename and template names have to specified in the  `names.txt` file. The first line is the name of the tex file (e.g., `gtd`), each following line specifies a template name. This means the number of lines in the `names.txt` file has to equal to the number of pages + 1 of the pdf file. 

The generated pdf can be converted using the `convert.py` script. The png/svg files and a templates.json file will be placed in the files directory. The templates can automatically be uploaded using the `upload.py` script or can be manually copied onto your remarkable.

Commands:
- `make pdf` generates pdf using `pdflatex`.
- `make convert` converts pdf to png and svg using (`pdfseparate`, `pdf2svg` and `rsvg-convert`).
- `make upload` uploads templates to remarkable and updates the `templates.json` file.
- `make clean` deletes latex build files and files directory.
- `make` runs `pdf`, `convert` and `upload` in sequence.

### Using Docker

You can also use `docker` to run all above commands without having the required dependencies installed on your computer.

Commands:
- `docker build -t gtd .` creates the docker image
- `docker run --network host -it gtd` executes the `make` command as documented above
- `docker run --network host -it gtd make pdf` to run a specific make command

## Notes
### Page Sizes
`pdf2svg` uses a dpi of 90.0

- Width: 1404 pixels = 15.6in
- Height: 1872 pixels = 20.8in
- Left: 120 pixels = 1.33in
- Top: 20 pixels = 0.22in
- Right: 20 pixels = 0.22in
- Bottom: 20 pixels = 0.22in
