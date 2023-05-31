# Fixes for terraformer

I needed terraformer to create better names for resources but saw no option in the program itself.

tf-names.py takes a plan file from terraformer, changes the resource names that it will create, and
 writes a fixed plan file.

Then you run terraformer on that like this: `terraformer import plan newplan.json`


After the import it's also necessary to change the provider name in the state file because it
contains the Terraform pre-0.13 variant.

I also couldn't find a way to write each hosted zone + records to its own file. Yet.

