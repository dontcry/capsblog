import React from 'react'
import { render } from 'react-dom' 
import { getBlogs } from './utils/api'
import { DatePicker } from 'antd';



class Hello extends React.Component {
    render() {
       return (
           <p>hello react</p>
        )
    }
}
let root = document.getElementById('root')
render(
    [<Hello/> ], root
) 
render(<DatePicker />, root);

getBlogs().then(res => {
    console.log(res)
  }).catch(err => {
    console.log(err) 
  })
 