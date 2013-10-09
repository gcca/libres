package gz;

import java.io.IOException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class SignInServlet extends HttpServlet {
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
            // NO CONSIDERAR ESTA IMPLEMENTACIÓN
            // NO SIRVE PARA EL FORM-AUTH
        resp.getWriter().println("Hola");
    }
}
