import sys, os.path, virtualenv, textwrap

def main(args):
    bootstrapdir = '.'
    if len(args) > 1:
        if os.path.exists(args[1]):
            bootstrapdir = args[1]
            print 'Creating bootstrap file in: "'+bootstrapdir+'"'
        else:
            print 'Directory "'+args[1]+'" does not exist. Placing bootstrap in "'+os.path.abspath(bootstrapdir)+'" instead.'

    output = virtualenv.create_bootstrap_script(textwrap.dedent(""""""))
    f = open(bootstrapdir+'/bootstrap.py', 'w').write(output)

if __name__ == '__main__':
    main(sys.argv)
