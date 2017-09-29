# imports for Jetty
from org.eclipse.jetty.server import Server
from org.eclipse.jetty.servlet import ServletHolder
from org.eclipse.jetty.webapp import WebAppContext
from org.eclipse.jetty.servlet import DefaultServlet

# imports for WtApplicationServlet
from eu.webtoolkit.jwt import WApplication
from eu.webtoolkit.jwt import WEnvironment
from eu.webtoolkit.jwt import WtServlet
from eu.webtoolkit.jwt import Configuration
from java.io import File

# import our Wt application
import WtApplication.application


class RunServerOptions:
    # DEBUG causes a reload of the application module for each new session. This is runtime expensive but allows hot-swapping code, useful for real time testing.
    DEBUG = True
    # Port for webserver
    ADDRESS_PORT = 8080
    # Name of configuration file for both Jetty and Wt
    CONFIGURATION_FILE = "web.xml"
    # Reference path for resources, "." indicates the same folder as runserver.py
    CONTEXT_RESOURCE_BASE = "."
    # Reference URL path for context, servlet paths are: http://hostname/contextPath/servletPath/pathInfo
    CONTEXT_PATH = "/"
    # Reference URL path for default servlet, useful to serve static files
    SERVLET_DEFAULT_URL = "/static/*"
    # Reference URL path for Wt
    SERVLET_WT_URL = "/*"
    # Enables or disables directory listing on default servlet
    CONTEXT_INIT_DIRALLOWED = "false"
    
    
class WtApplicationServlet(WtServlet):
    def __init__(self):
        WtServlet.__init__(self)
        print("[WtJython] Instancing Wt Application Servlet")
        self.setConfiguration(Configuration(File(RunServerOptions.CONFIGURATION_FILE)))
        
    def createApplication(self, wenvironment):
        if RunServerOptions.DEBUG == True:
            reload(WtApplication.application)
        return WtApplication.application.MyWtApplication(wenvironment)

        
def main():
    try:
        # Initialize Jetty server at desired port
        print("[WtJython] Starting server at port " + str(RunServerOptions.ADDRESS_PORT))
        server = Server(RunServerOptions.ADDRESS_PORT)        

        # Initialize context and setup general options
        context = WebAppContext()
        context.setDescriptor(RunServerOptions.CONFIGURATION_FILE)
        context.setResourceBase(RunServerOptions.CONTEXT_RESOURCE_BASE)
        context.setContextPath(RunServerOptions.CONTEXT_PATH)
        #context.setParentLoaderPriority(True) # use standard Java classloader behavior before WebApp (NOT NECESSARY?)
        context.setInitParameter("org.eclipse.jetty.servlet.Default.dirAllowed", RunServerOptions.CONTEXT_INIT_DIRALLOWED)
        
        # servlet for static contents
        context.addServlet(ServletHolder(DefaultServlet()), RunServerOptions.SERVLET_DEFAULT_URL)
        
        # servlet for Wt application
        context.addServlet(ServletHolder(WtApplicationServlet()), RunServerOptions.SERVLET_WT_URL)
        
        # Note: filters should be added here. Wt uses Servlet 3.0 API and as such it uses asynchronous responses. Filters should use response.getAsyncContext().AddListener .

        # Set our context, start server and wait for shutdown
        server.setHandler(context)
        server.setStopAtShutdown(True)
        server.start()
        server.join()
    except Exception as e:
        print("[WtJython] Exception caught in main(): " + str(e))
        
        
if __name__ == "__main__":
    main()