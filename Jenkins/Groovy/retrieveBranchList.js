def gitURL = "git@github.wdf.sap.corp:OnePortal/panda-main.git"
def command = "git ls-remote -h $gitURL"

def proc = command.execute()
proc.waitFor()              

if ( proc.exitValue() != 0 ) {
   println "Error, ${proc.err.text}"
   System.exit(-1)
}

def branches = proc.in.text.readLines().collect { 
    it.replaceAll(/[a-z0-9]*\trefs\/heads\//, '') 
}

assert branches == branches.sort(java.text.Collator.instance)
println branches
def list = branches