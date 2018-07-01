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
- In spyder, run tabulation_plot, changing filenames to the ones data was stored in.
# Tabulation data is stored in code/data, with filenames initialflavor-Q0-Q-dy-dlnlnQ.txt
