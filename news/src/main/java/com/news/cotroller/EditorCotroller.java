package com.news.cotroller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.news.dao.PostsDao;
import com.news.dao.TargetDao;
import com.news.entity.Posts;
import com.news.entity.Target;
import com.news.entity.User;
import com.news.utils.EditorInfo;

@Controller
@RequestMapping("Editor")
public class EditorCotroller {
	
	@Autowired
	TargetDao tardao;
	
	@Autowired
	PostsDao postsdao;
	
	public User auth(HttpServletRequest req) {
		HttpSession s = req.getSession();
		User user = (User)s.getAttribute("user");
		if(user != null) return user;
		return null;
	}
	
	@RequestMapping("index")
	public String index(ModelMap m) {
		m.put("val", -1);
		return "Editor/index";
	}
	
	@RequestMapping("update")
	public String update(int id, ModelMap m) {
		m.put("val", id);
		return "Editor/index";
	}
	
	@RequestMapping("target")
	public @ResponseBody List<Target> target() {
		return tardao.select();
	}
	
	@RequestMapping("get")
	public @ResponseBody Posts get(int id) {
		return postsdao.getPosts(id);
	}
	
	
	@RequestMapping("add")
	public @ResponseBody EditorInfo add(@RequestBody Posts p, HttpServletRequest req) {
		User user = auth(req);
		if(user == null) return new EditorInfo("error", "请先登录");
		p.setUserid(user.getId());
		if(p.getId() != -1) {
			postsdao.update(p);
		} else {
			postsdao.insert(p);
		}
		return new EditorInfo("success", "");
	}
}
