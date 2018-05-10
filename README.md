# Delta Function evolution. To do setup do the following.
- source setup
- cd code/hoppet/
- ./configure --prefix="..."  FC="..."
# (If this give you an error. Run ./configure)
- make
- make check

# To get a plot:
- cd code/hoppet/delta_evo
# Modify delta_tabulation.cc as desired
- make
- ./delta_tabulation
- spyder ../../Python/tabulation_plot.py
- In spyder, run tabulation_plot.
# Currently only one dataset is stored at a time, so tabulation_plot automatically plots whatever the last result from delta_tabulation was.
