settings.tex = "xelatex";
usepackage("ctex");
settings.outformat = "pdf";
size(5cm,0);
pair z1 = (0,1), z2 = (1,1), z3 = (2,1),
z4 = (0,0), z5 = (1,0), z6 = (2,0);
path p = z4 .. z1 .. z2 .. z6;
draw(p, gray+2mm);