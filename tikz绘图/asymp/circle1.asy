settings.outformat="pdf";
unitsize(2cm);
import graph;
// path line = (0,0) -- (1,1);
// dot((3,3));
// dot((0,0),red);

// draw(scale(2)*line,red);
// draw(line,blue);
path e1 = ellipse((0,0),1,0.5);
path e2 = ellipse((0,0),0.5,1);
draw(circle((0,0),1));
draw(subpath(e1,0,2),dashed);
draw(subpath(e1,2,4));
draw(subpath(e2,-1,1),dashed);
draw(subpath(e2,1,3));
// draw(subpath(e2,2,4));