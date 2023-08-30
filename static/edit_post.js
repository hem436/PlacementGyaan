const base_url = window.location.href.substring(0,25)
const edit_post=new Vue({
    el:"#app",
    data() {
        return {
            conn_list:JSON.parse(sessionStorage.getItem('conn_list')),
            myprofile:JSON.parse(sessionStorage.getItem('myprofile')),
            currentPost:JSON.parse(sessionStorage.getItem('currentPost')),
        }
    },
    methods: {
        'submitPost': function(){
            console.log("create post function");
            const formData = new FormData();
                formData.append('post_id',this.currentPost.post_id)
                formData.append("experiences", this.currentPost.experiences)
                formData.append('tips',this.currentPost.tips)
            fetch(`${base_url}/api/posts`,{
                method:'PUT',
                body:formData,
            })
            .then((res)=>{
                sessionStorage.removeItem('currentPost')
                window.location.href=`./dashboard/${this.myprofile.user_id}`
            })
            .catch((error)=>{alert(error.message)})
        },
        dashBoard:function () {
            window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
        },
    },
    created() {
        console.log(this.currentPost);
    },
})