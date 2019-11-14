import { Button, Input, message, Select } from "antd";
import { default as highlight, default as hljs } from "highlight.js";
import marked from "marked";
import React from "react";
import SimpleMDE from "simplemde";
import axios from "axios";
import config from "./config";
import "simplemde/dist/simplemde.min.css";

const Option = Select.Option;

export default class Editor extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      smde: null,
      body: "",
      title: "",
      category: 1,
      categories: []
    };
  }

  componentWillMount() {
    marked.setOptions({
      renderer: new marked.Renderer(),
      gfm: true,
      tables: true,
      breaks: true,
      pedantic: false,
      sanitize: true,
      smartLists: true,
      smartypants: false,
      highlight: function(code) {
        return hljs.highlightAuto(code).value;
      }
    });
    axios.get(config.get_url).then(response => {
      console.log(response.data.data);
      this.setState({
        categories: response.data.data,
      });
    });
  }

  componentDidMount() {
    let smde = new SimpleMDE({
      element: document.getElementById("editor").childElementCount,
      autofocus: true,
      autosave: true,
      previewRender(plainText) {
        return marked(plainText, {
          renderer: new marked.Renderer(),
          gfm: true,
          pedantic: false,
          sanitize: false,
          tables: true,
          breaks: true,
          smartLists: true,
          smartypants: true,
          highlight(code) {
            return highlight.highlightAuto(code).value;
          }
        });
      }
    });
    this.setState({
      smde: smde
    });
  }

  handleOnClick() {
		let data = {
			title: this.state.title,
			category_id: this.state.category,
			body: marked(this.state.smde.value())
		}

		if(!data.title) {
			message.warn('标题不能为空');
			return ;
		}
		else if(!data.category_id) {
			message.warn('类型不能为空')
			return ;
		}
		else if(!data.body) {
			message.warn('文章不能为空');
			return ;
		}
		
		axios
      .post(config.post_url, data)
      .then(response => {
        let data = response.data;
        console.log(response.data);
        if (data.type == "error") {
          message.warn(data.message);
        } else if (data.type == "success") {
          message.success(data.message);
        }
      })
      .catch(error => {
        console.log(error);
        message.info("Error, Something wrong");
      });
  }

  handleTitleChange(event) {
    this.setState({
      title: event.target.value
    });
  }

  handleTypeChange(value) {
    console.log(value);
    this.setState({
      category: value
    });
  }

  render() {
    let categories_list = this.state.categories.map((data, i) => {
      return (
        <Option value={data.id} key={i}>
          {data.name}
        </Option>
      );
    });
    return (
      <div>
        <Input
          style={{ margin: "10px 0", height: "40px" }}
          value={this.state.title}
          onChange={this.handleTitleChange.bind(this)}
        />

        <Select
          defaultValue={this.state.category}
          size="large"
          style={{ width: "100%", margin: "10px 0" }}
          onChange={this.handleTypeChange.bind(this)}
        >
          {categories_list}
        </Select>
        <textarea id="editor" style={{ padding: "10px 0" }} />
        <div style={{ textAlign: "center" }}>
          <Button
            onClick={this.handleOnClick.bind(this)}
            style={{ textAlign: "center" }}
          >
            提交
          </Button>
        </div>
      </div>
    );
  }
}
