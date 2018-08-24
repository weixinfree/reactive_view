## ReactiveView for Mobile develop

### 语法
```js
# this is comment
using com.demo.viewModel.UserViewModel as user

Column {
    w: match
    h: wrap
    gravity: center
    child: Text {
        w: 30dp
        # should use wrap
        h: 20dp
        textSize: 13sp
        text: {user.name |> title}
        visible: {user.name |> len |> gt $, 0}
        onClick: {v -> user.onClick}
        onItemClick: {view, position -> user.onItemClick}
    },
    child: Image {
        placeHolder: @drawable/default_portrait
        scaleType: fitCenter
        src: {user.portrait |> scale $, 30dp, 40dp}
    }
    child: include(../../names.vv)
}
```