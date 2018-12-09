### A DEVS Proof of Concept for calculating Dynamic Voronoi Diagrams

Also, this includes yet another PoC: A DEVS Wrapper, that by using and exploiting Jupyter and NumPy capabilities, is able to render animated plots of the simulation made with CellDEVS.

In order to use both the notebooks and the python modules, one has to use a custom version of the CD++ DEVS Simulator. The changes introduced add the possibility of exporting the drawlog-generated animations as CSV files, to make them easier to be parsed by a Python script. The repository containing this custom version of the CD++ simulator is [here](https://github.com/plbalbi/CDPP_ExtendedStates-codename-Santi/tree/DrawlogToNumpy).

For the modules to work, the underlying OS has to have in the PATH enviromental variable, the executable binaries of both the *CD++* simulator, and the *Drawlog* tool.

### Future improvements
- Dockerize all the framework, in order to make piping between the simulator, drawlog and the notebook itself easier.
- Maybe add some kind of object storage, or relational database, to avoid dumping log, model, and drawn files in /tmp.
- VTime wrapper.
- Testing.
- Error checking for the simulator in PATH envvar.
- There's a lot of boilerplate in the notebook to make the animations of the Voronoi use-case. This need changes.
- Rethink how the model files are generated.