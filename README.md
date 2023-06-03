# Fixes for terraformer

I needed terraformer to create better names for resources but saw no option in the program itself.

tf-names.py takes a plan file from terraformer, changes the resource names that it will create, and
 writes a fixed plan file.

Then you run terraformer on that like this: `terraformer import plan newplan.json`


After the import it's also necessary to change the provider name in the state file because it
contains the Terraform pre-0.13 variant.


To separate multiple zones to own files:

```sh
for domain in `grep zone route53_zone.tf | awk '{print $3}' | tr -d '"' ` ; do
  grep -E --no-group-separator -A 5 $domain route53_zone.tf >zone${domain}.tf
  grep -E --no-group-separator -A 7 "aws_route53_record.*${domain}" route53_record.tf >> zone${domain}.tf
  grep -E --no-group-separator -A 3 "output.*${domain}" outputs.tf >> zone${domain}.tf
done
```

(requires GNU grep, on OS X install it with brew, it will be available as ggrep)

