# DBiharmonic


This was the first ratcheting simulation to be run once DLattice was first created.
Unfortunately, it has not yet been revamped like DLattice still includes a lot of artifacts.
In the future, this will see a number of changes to make it a bit more distinct.
Namely, 'a.out' as the executable is a very terrible name, and 'FortranRunner.sh' is not great either.
These just don't specify what program they're supposed to be working with.

But let's imagine you don't care about any of that and just want to see some data.
I too, hate code...
You'll have to start by compiling the Fortran file on your computer.
This requires that you have MPICH somewhere on there as well.
Start by navigating to the folder than the Fotran file is in then type.
  mpifort -o a.out DBiharmonic.f
If you're coming from DLattice, you'll notice the output file is called 'a.out'
This is very sloppy because it doesn't explain which program it came from.

From here, check through the InputStart and BiharmShell2.sh to check the input parameters.
You'll want to set them to what values you want.
Force and Gamma are determined in the base script, InputStart determines the others.
If you want to change the A and B values for the force, this still has to be done in the Fortran.
Again, it's sloppy and needs changed.

Once it's all set you have just to run the main bash script.
Start by giving them all permission to run
  chmod +x ./'Filename'
And then just run the main shell
  ./BiharmShell2.sh
Which will make a bunch of folders and spit out a bunch of data.

Now you can just use the plotting program to plot all of this.
This is explained inside of the comments of the plotter, but you should just select the folder with all of the data folders in it.
It will automatically look through these folders and pull all of the data as long as you haven't changed names.
