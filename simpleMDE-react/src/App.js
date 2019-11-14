import { Icon, Layout, Menu, Modal } from "antd";
import React, { Component } from "react";
import "./App.css";
import config from "./config";
import Editor from "./Editor";

const { Header, Content, Footer } = Layout;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visable: false
    };
  }

  handleShowModle() {
    this.setState({
      visable: true
    });
  }

  handleOnBack() {
    window.open(config.index_page_url, "_self");
  }

  handleOnReturn() {
    this.setState({
      visable: false
    });
  }

  render() {
    return (
      <Layout className="layout">
        <Header>
          <div className="logo" />
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={["2"]}
            style={{ lineHeight: "64px" }}
          >
            <Menu.Item key="1">
              <div onClick={this.handleShowModle.bind(this)}>
                <Icon type="arrow-left" />
                返回
              </div>
            </Menu.Item>
          </Menu>
        </Header>
        <Modal
          title="确定放弃所有更改并返回吗?"
          visible={this.state.visable}
          onOk={this.handleOnBack.bind(this)}
          onCancel={this.handleOnReturn.bind(this)}
          okText="确定"
          cancelText="取消"
        />
        <Content style={{ padding: "0 50px" }}>
          <br />
          <h2>创建文章</h2>
          <Editor/>
        </Content>
        <Footer style={{ textAlign: "center" }}>Bluelog ©2018</Footer>
      </Layout>
    );
  }
}

export default App;
