# Configurator API Merge Template

## Quick Start
This is a template to create a custom configurator_api for your system. To use this template, create a new repo using this template, then clone down your new repo. Edit the product.yaml and catalog.yaml files found in .stage0_template/Specifications/ and then use the ``make merge`` command as shown below. 
```sh
## Merge your specifications with the template
make merge .stage0_template/Specifications
```
And then you should have a functional Schema Manager of your very own. Refresh you view of the README for more information, or just run ``make dev`` to start working with your schema's.

## Contributing
See [Template Guide](https://github.com/agile-learning-institute/stage0_runbook_merge/blob/main/TEMPLATE_GUIDE.md) for information about stage0 merge templates. See the [Processing Instructions](./.stage0_template/process.yaml) for details about this template, and [Test Specifications](./.stage0_template/Specifications/) for sample context data required.

Template Commands
```sh
## Test the Template using test_expected output
## Creates ~/tmp folders 
make test
## Successful output looks like
...
Checking output...
Only in /Users/you/tmp/testRepo: .git
Only in /Users/you/tmp/testRepo/configurator: .DS_Store
Done.

## Clean up temp files from testing
## Removes tmp folders
make clean

## Process this merge template using the provided context path
## NOTE: Destructive action, will remove .stage0_template 
## Context path typically ends with ``.Specifications``
make merge {context path}
```
