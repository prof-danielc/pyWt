Tips:

1) Additional resources can be made accessible by JWt by exploring Java's classpath on eu.webtoolkit.jwt.wt-resources

For this, it's necessary to:

a) have the folder tree eu/webtoolkit/jwt/wt-resources on the base path
b) run jython with the flag -J-cp "WHATEVER;./"

Then, anything that is added to eu/webtoolkit/jwt/wt-resources can be accessed by Wt. Resources were made available in this fashion before a specific servlet for static resources was created.