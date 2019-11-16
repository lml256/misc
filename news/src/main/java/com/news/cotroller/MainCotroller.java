package com.news.cotroller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.news.dao.PostsDao;
import com.news.dao.TargetDao;
import com.news.dao.UserDao;
import com.news.entity.Posts;
import com.news.entity.Target;
import com.news.entity.User;
import com.news.utils.SearchInfo;

@Controller
@RequestMapping("Main")
public class MainCotroller {
	
	@Autowired
	PostsDao dao;
	
	@Autowired
	UserDao userdao;
	
	@Autowired
	TargetDao targetdao;
	
	public User auth(HttpServletRequest req) {
		HttpSession s = req.getSession();
		User user = (User)s.getAttribute("user");
		if(user != null) return user;
		return null;
	}
	
	@RequestMapping("index")
	public String index(SearchInfo info, ModelMap m, HttpServletRequest req) {
		List<Posts> list = dao.select(info);
//		for(int i = 0; i < list.size(); i++) {
//			System.out.println(list.get(i));
//		}
		m.put("news", dao.select(info));
		m.put("search", info);
		m.put("user", auth(req));
		return "Main/index";
	}
	
	@RequestMapping("delete")
	public String delete(int id, ModelMap m, HttpServletRequest req) {
		dao.delete(id);
		return "redirect:index";
	}
	
	@RequestMapping("show")
	public String show(int id, ModelMap m) {
		m.put("id", id);
		return "Main/show";
	}
	
	@RequestMapping("info")
	public String info(ModelMap m) {
		return "Main/info";
	}
	
	@RequestMapping("update")
	public String update(@RequestParam(defaultValue="",value="pass") String pass, ModelMap m, HttpServletRequest req) {
		User user = auth(req);
		System.out.println(user);
		if(user != null) {
			user.setPass(pass);;
			userdao.update(user);
		}
		return "Main/info";
	}
	
	@RequestMapping("titleSearch")
	public String titleSearch(@RequestParam(defaultValue="",value="title") String title, SearchInfo info, ModelMap m, HttpServletRequest req) {
		if(title.equals("")) return "Main/titleSearch";
		info.setWhere(" and title like '%"+title+"%' ");
		info.setLimit("");
		List<Posts> posts = dao.select(info);
		m.put("list", posts);
		m.put("user", auth(req));
		return "Main/scheam";
	}
	
	@RequestMapping("authorSearch")
	public String authorSearch(@RequestParam(defaultValue="",value="username") String name, SearchInfo info, ModelMap m) {
		if(name.equals("")) return "Main/authorSearch";
		info.setWhere(" and user.name='" + name + "' ");
		info.setLimit("");
		List<Posts> list = dao.select(info);
		m.put("list", list);
		return "Main/scheam";
	}
	
	@RequestMapping("typeSearch")
	public String typeSearch(@RequestParam(defaultValue="-1",value="value") int id, SearchInfo info, ModelMap m) {
		System.out.println(id);
		if(id == -1) {
			List<Target> tlist = targetdao.select();
			m.put("tlist", tlist);
			return "Main/typeSearch";
		}
		info.setLimit("");
		info.setWhere(" and target ="+id+" ");
		List<Posts> list = dao.select(info);
		m.put("list", list);
		return "Main/scheam";
	}
	
	@RequestMapping("search")
	public String search(SearchInfo info, ModelMap m) {
		return "Main/search";
	}
}
