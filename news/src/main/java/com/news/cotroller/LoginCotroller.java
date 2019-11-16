package com.news.cotroller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;

import com.news.dao.UserDao;
import com.news.entity.User;

@Controller
@RequestMapping("Login")
public class LoginCotroller {
	
	@Autowired
	UserDao dao;
	
	@RequestMapping("login")
	public String login(User u, ModelMap m, HttpServletRequest req) {
		System.out.println(u.getName());
		int v = dao.login(u);
		System.out.println("v: " + v);
		if(v > 0) {
			HttpSession s=req.getSession();
			s.setMaxInactiveInterval(100000);
			s.setAttribute("user", u);
			return "redirect:../index";
		}
		return "Login/login";
	}
	
	@RequestMapping("signup")
	public String signup() {
		return "Login/signup";
	}
	
	@RequestMapping("logout")
	public String logout(HttpServletRequest req) {
		HttpSession s = req.getSession();
		s.removeAttribute("user");
		return "redirect:login";
	}
	
	@RequestMapping("add")
	public String add(User u, ModelMap m) {
		dao.insert(u);
		return "Login/login";
	}
}
