import React from 'react';
import { Spin } from 'antd';

export default class Loading extends React.Component {
  render () {
    const style = {
      color: '#999',
      textAlign: 'center'
    }
    return (
      <div style={style}>
        <Spin size="large" />
      </div>
    )
  }
}