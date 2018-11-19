This is an app to test deployment of pmml files. 

The process followed was : 

1. Build a simple decision tree classifier on the classic iris dataset.
2. Create a PMML file of this classifier and host it using openscoring library. The git link is here : 
     https://github.com/openscoring/openscoring-python
3.  Build a basic DASH application. [ If you might be wondering what is dash, here is the link -  https://plot.ly/products/dash/
4. In this DASH app call the openscoring function and in real time score the data. 
