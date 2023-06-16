# print data on a file every 0.09 ps
declare_output(
    name = "$JOBNAME.cvseq",
    first = 0.000000,
    interval= 0.090000);

# center of mass of the ligand - it is a coordinate xyz 

cv_00_g0 = center_of_mass ( atomsel("ligand and not atom.ele H ") );

# center of mass of the protein (calphas) - it is a coordinate xyx
cv_00_g1 = center_of_mass ( atomsel("protein and atom.ptype CA") );

# calculate the difference in the coordinate, 
# wrap back in the same box and calculate the norm of  the resulting vector 
cv_00 = norm(min_image(cv_00_g0 - cv_00_g1));

# print on the file (see declare_output)
print ("cv_00", cv_00);

# an harmonic potential with initial center at 7.3
x_0 = 7.3;
# positive speed: CV is increased
speed_cv_per_ps=0.1;
# increase the value of the center of harmonic potential linearly with time
center_harm = x_0+speed_cv_per_ps*time() ;
print("center_harm",center_harm);
# hamonic potential
delta = cv_00 - center_harm ;
harm = 500*delta*delta ;

print ("harm", harm);
# WARNING!!! LAST LINE IS THE POTENTIAL!!! 
# just zero for the time being. Simulation is not bias 
harm;
