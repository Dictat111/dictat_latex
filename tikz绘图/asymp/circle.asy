settings.outformat = "pdf";
size(6cm);

draw((0,0) -- (1,1) -- (2,sqrt(2)));

draw((0,0)    .. (1,1) .. (2,sqrt(2))); // 软的线
draw(circle((0,1), 0.5), red);

draw((-0.1,0) -- (2,0), arrow=Arrow);
draw((0,-.1) -- (0,2), arrow = Arrow);

draw(unitcircle,green);
draw(polygon(3), blue);