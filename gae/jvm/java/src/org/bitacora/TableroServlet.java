package bitacora;

import java.io.IOException;
import javax.servlet.http.*;

public class TableroServlet extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        resp.setContentType("text/plain");
        resp.getWriter().println("Hola a todos");
    }
}
