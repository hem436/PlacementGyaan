const base_url = window.location.href.substring(0,25)
//import load_post from "./posts.js"

const new_post=new Vue({
    el:"#app",
    data() {
        return {
            myprofile:JSON.parse(sessionStorage.getItem('myprofile')),
            conn_list:JSON.parse(sessionStorage.getItem('conn_list')),
            experiences:'',
            tips:''
        }
    },
    methods: {
        'createPost': function(){
            console.log("create post function");
            const formData = new FormData();
                formData.append('user_id',this.myprofile.user_id)
                formData.append("experiences", this.experiences)
                formData.append('tips',this.tips)
            fetch(`${base_url}/api/posts`,{
                method:'POST',
                body:formData,
            })
            .then((res)=>{
                window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
            })
            .catch((error)=>{alert(error.message)})
        },
        dashBoard:function () {
            window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
        },
    },
    created() {
        console.log('experiences',this.experiences)
        console.log('create js loaded')
    },
})