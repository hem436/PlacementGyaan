const base_url = window.location.href.substring(0,25)

const all_post = new Vue({
    el:"#app",
    data(){
        return{
        myprofile:JSON.parse(sessionStorage.getItem('myprofile')),
        conn_list:JSON.parse(sessionStorage.getItem('conn_list')),
        post_list:[],
        currentPage:1,
        }
    },
    computed: {
        totalPages(){
            return this.post_list.length
        },
        currentPost(){
            return this.post_list[this.currentPage-1] || {}
        }
    },
    methods: {
        nextPage:function(){
            // console.log('inside next Pae');
            if (this.currentPage < this.totalPages){this.currentPage++}
        },
        previousPage:function(){
            // console.log('inside pre page');
            if (this.currentPage > 1){this.currentPage--}
        },
        editPost:function(){
            sessionStorage.setItem('currentPost',JSON.stringify(this.currentPost))
            window.location.href=`${base_url}/edit_post`
        },
        dashBoard:function () {
            window.location.href=`${base_url}/dashboard/${this.myprofile.user_id}`
        },
        'load_post':function(){
            fetch(`/api/0/posts/${this.myprofile.user_id}`,{
                method:"GET"
            })
            .then((res)=>{if(res.ok){return res.json()}
                        else{throw new Error(res.text())}})
            .then((data)=>{
                data.posts.forEach(element=>{
                    this.post_list.push(element)
                })
            })
            .catch((err)=>{ console.log(err.message);})
            
            if(this.conn_list.length > 0){
                this.conn_list.forEach(element => {
                    fetch(`${base_url}/api/0/posts/${element}`,{
                    method:"GET"
                })
                .then((res)=>{if(res.ok){return res.json()}
                            else{console.log(res.text());}})
                .then((data)=>{
                    data.posts.forEach(element=>{
                        this.post_list.push(element)
                    })
                })
                .catch((err)=>{ console.log(err.message);})
                });
            }
        },
        'deletePost':function(){
            fetch(`${base_url}/api/posts/${this.currentPost.post_id}`,{
                method:"DELETE",
            })
            location.reload()
        },
    },
    created(){
        this.load_post()
        console.log('posts',this.post_list)
    },
})
