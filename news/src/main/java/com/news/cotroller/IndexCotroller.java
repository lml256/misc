package com.news.cotroller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class IndexCotroller {
	
	@RequestMapping("index")
	public String index(ModelMap m, HttpServletRequest req) {
		HttpSession s = req.getSession();
		if(s.getAttribute("user") != null) {
			m.put("user", s.getAttribute("user"));
		}
		return "index";
	}
}
