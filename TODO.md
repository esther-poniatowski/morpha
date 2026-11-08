# TODO

Items are grouped by the condition that opens them.

## Defects observed against the layout of project repositories

The assessment of 2026-11-08 checked Morpha against the common layout of the project repositories of Geonexus. Morpha fits that layout, since every path comes from its caller. The following defects of Morpha itself would harm a project that uses it.

- [ ] **Keep a dot inside the stem of a file name.** `IOHandler.__init__`, in `src/morpha/io/base.py`, calls `path.with_suffix` whenever the suffix of the path is not an extension of the handler. A stem that holds a dot therefore loses its end: `SaverPKL("run_lr0.5")` writes `run_lr0.pkl`, and `"sess.2024-01"` writes `sess.pkl`. A known but wrong extension is replaced silently: `"a.npy"` becomes `a.pkl` for the pickle saver. Append the extension when the suffix is unknown, raise when the suffix is the extension of another format, and test both cases.
- [ ] **Save a `DataComponent` with its names.** A pickled `DataComponent` keeps its class but loses its dimensions and its metadata, since the class defines neither `__reduce__` nor `__setstate__`. The savers of NPY, NPZ and HDF5, in `src/morpha/io/savers.py`, store bare arrays. Support pickling, and store the dimensions and the metadata as attributes in NPZ and HDF5.
- [ ] **Give `DataStructure` a route to save and load.** A `DataStructure` has no save method, so a composite container cannot be written as one file.
- [ ] **Decide whether a saver creates its folder.** `Saver.__init__`, in `src/morpha/io/savers.py`, raises `FileNotFoundError` when the parent folder is missing. Either create the folder on request, or document that the caller creates it.
- [ ] **Align the extensions with the savers.** The extensions of `src/morpha/io/base.py` admit `.csv`, but no saver writes CSV. Remove the extension, or add a saver and a loader of CSV.
