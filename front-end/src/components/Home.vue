<template>
  <div class="container">

    <!-- Modal: Edit Post -->
    <div class="modal fade" id="updatePostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="updatePostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form @submit.prevent="onSubmitUpdate" @reset.prevent="onResetUpdate">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editForm.titleError}">
                <input type="text" v-model="editForm.title" class="form-control" id="editform_title" placeholder="标题">
                <small class="form-control-feedback" v-show="editForm.titleError">{{ editForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editForm.summary" class="form-control" id="editform_summary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editForm.body" class="form-control" id="editform_body" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editForm.bodyError">{{ editForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

          </div>
        </div>
      </div>
    </div>

    <form v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAdd" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
        <input type="text" v-model="postForm.title" class="form-control" id="post_title" placeholder="标题">
        <small class="form-control-feedback" v-show="postForm.titleError">{{ postForm.titleError }}</small>
      </div>
      <div class="form-group">
        <input type="text" v-model="postForm.summary" class="form-control" id="post_summary" placeholder="摘要">
      </div>
      <div class="form-group">
        <textarea v-model="postForm.body" class="form-control" id="post_body" rows="5" placeholder=" 内容"></textarea>
        <small class="form-control-feedback" v-show="postForm.bodyError">{{ postForm.bodyError }}</small>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Posts <small v-if="posts">(共 {{ posts._meta.total_items }} 篇, {{ posts._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>

          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="posts" class="card-block g-pa-0" >
        <post v-for="(post, index) in posts.items" v-bind:key="index"
          v-bind:post="post"
          v-on:edit-post="onEditPost(post)"
          v-on:delete-post="onDeletePost(post)">
        </post>
      </div>
      <!-- End Panel Body -->
    </div>

    <!-- Pagination #04 -->
    <div v-if="posts">
      <pagination
        v-bind:cur-page="posts._meta.page"
        v-bind:per-page="posts._meta.per_page"
        v-bind:total-pages="posts._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->

  </div>
</template>

<script>
import store from '../store'
import Post from './Base/Post'
import Pagination from './Base/Pagination'
import '../assets/bootstrap-markdown/js/bootstrap-markdown'
import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh'
import '../assets/bootstrap-markdown/js/marked'

export default {
  name: 'Home',
  components: {
    Post,
    Pagination
  },
  data() {
    return {
      sharedState: store.state,
      posts: '',
      postForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      editForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      }
    }
  },
  methods: {
    getPosts() {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }
      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      const path = `/posts?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          this.posts = response.data
        })
        .catch((error) => {
          console.log(error.response.data)
        })
    },
    onSubmitAdd(e) {
      this.postForm.errors = 0
      if (!this.postForm.title) {
        this.postForm.errors++
        this.postForm.titleError = 'Title is required.'
      } else {
        this.postForm.titleError = null
      }

      if (!this.postForm.body) {
        this.postForm.errors++
        this.postForm.bodyError = 'Body is required.'
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')
      } else {
        this.postForm.bodyError = null
      }

      if (this.postForm.errors > 0) {
        return false
      }

      const path = '/posts'
      const payload = {
        title: this.postForm.title,
        summary: this.postForm.summary,
        body: this.postForm.body
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getPosts()
          this.$toasted.success('Add new post successed.')
          this.postForm.title = ''
          this.postForm.summary = ''
          this.postForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onDeletePost(post) {
      this.$swal({
        title: "Are you sure?",
        text: "It will completely delete [ " + post.title + " ], be careful!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonColor: 'No, cancel!'
      }).then((result) => {
        if (result.value) {
          const path = `/posts${post.id}`
          this.$axios.delete(path)
            .then((response) => {
              //handle success
              this.$swal('Deleted', 'You successfully deleted this post', 'success')
              this.getPosts()
            })
            .catch((error) => {
              //handle error
              console.log(error.response.data)
            })
        } else {
          this.$swal('Cancelled', 'The post is safe', 'error')
        }
      })
    },
    onEditPost(post) {
      this.editForm = Object.assign({}, post)
    },
    onSubmitUpdate() {
      this.editForm.errors = 0
      $('.form-control-feedback').remove()
      $('.form-group.u-has-error-v1').removeClass('u-has-error-v1')
      if (!this.editForm.title) {
        this.editForm.errors++
        this.editForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editform_title').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editform_title').after('<small class="form-control-feedback">' + this.editForm.titleError + '</small>')
      } else {
        this.editForm.titleError = null
      }
      if (!this.editForm.body) {
        this.editForm.errors++
        this.editForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('.md-editor').after('<small class="form-control-feedback">' + this.editForm.bodyError + '</small>')
      } else {
        this.editForm.bodyError = null
      }
      if (this.editForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }
      // 先隐藏 Modal
      $('#updatePostModal').modal('hide')
      const path = `/posts/${this.editForm.id}`
      const payload = {
        title: this.editForm.title,
        summary: this.editForm.summary,
        body: this.editForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPosts()
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editForm.title = '',
          this.editForm.summary = '',
          this.editForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onResetUpdate() {
      $('.form-control-feedback').remove()
      $('.form-group.u-has-error-v1').removeClass('u-has-error-v1')
      $('#updatePostModal').modal('hide')
      this.$toasted.info('Cancelled, the post is not update.', {icon: 'fingerprint'})
    }
  },
  created () {
    this.getPosts()
    // Initialize bootstrap-markdown plugin
    $(document).ready(function() {
      $("#post_body, #editform_body").markdown({
        autofocus: false,
        savable: false,
        iconlibrary: 'fa',
        language: 'en'
      })
    })
  },
  beforeRouteUpdate(to, from, next) {
    next()
    this.getPosts()
  }
}
</script>
