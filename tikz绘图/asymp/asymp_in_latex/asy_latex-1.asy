if(!settings.multipleView) settings.batchView=false;
settings.tex="xelatex";
defaultfilename="asy_latex-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

// 定义 Asymptote 代码
size(100);
draw(unitcircle);
