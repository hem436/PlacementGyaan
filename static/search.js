const base_url = window.location.href.substring(0,25)

const sear=new Vue({
    el:"#app",
    data() {
        return {
            match_list:[],
            keyword:''
        }
    },
    methods: {
        'follow': function(item){
            fetch(`${base_url}/api/${this.myprofile.user_id}/connection/${item.user_id}`,{
                method:'POST',
                credentials:'same-origin'
            })
            .then(() => {
                alert(`You are now following ${item.username}`)
                location.reload()
            })
            .catch((err) => {alert(err.message)})
            },
        'unfollow': function(item){
            fetch(`${base_url}/api/${this.myprofile.user_id}/connection/${item.user_id}`,{
                method:'DELETE',
                credentials:'same-origin'
            })
            .then((response) => {
                alert(`You are no longer following ${item.username}`)
                location.reload()
            })
            .catch((err) => {alert(err.message)})
            },
        'find':function(){
                fetchFunction(`${base_url}/api/search/${this.keyword}`,'GET')
                .then((res)=>{this.match_list=res.matches})
                .catch((err) => {alert(err.message)})
        },
        go_to_user(user_id){
            window.location.href=`${base_url}/${user_id}/user_page/${myprofile.user_id}`
        }
    },
})