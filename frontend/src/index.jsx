import React from 'react'
import { render } from 'react-dom' 
import { getBlogs } from './utils/api'
class Hello extends React.Component {
    render() {
       return (
           <p>hello react111223334444！</p>
        )
    }
}
render(
    [<Hello/> ],
    document.getElementById('root')
) 


getBlogs().then(res => {
    console.log(res)
  }).catch(err => {
    console.log(err) 
  })
 