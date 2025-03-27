

### 1. Goal of the project
The goal is to sort photos based on time-stamps. It looks like the sort function is well developed.

### 2. The input data
Is one or more folders/cards of images. Do the images need to be any particular format. 
This should be stated in the README. You could insert checks to ensure the data is properly
formatted.

### 3. Functions
There is a well developed skeleton for the future functions. I would recommend looking
into the options for developing the command-line interface using "subcommands" in argparse,
rather than combining all of the CLI commands into a single command with many options that
only apply to one step or another. As separate subcommands you can provide only options that are 
only relevant to each step.
