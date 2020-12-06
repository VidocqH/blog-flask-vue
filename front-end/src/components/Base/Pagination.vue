<template>

  <nav aria-label="Page Navigation" class="g-mb-50">
    <ul class="list-inline">
      <li class="list-inline-item">
        <router-link v-bind:to="{ path: $route.path, query: { page: curPage - 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == 1}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Previous">
          <span aria-hidden="true">
            <i class="fa fa-angle-left"></i>
          </span>
          <span class="sr-only">Previous</span>
        </router-link>
      </li>
      <div v-if="page != 'NaN'">
       <li v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item g-hidden-sm-down">
          <router-link v-bind:to="{ path: $route.path, query: { page: page, per_page: perPage }}" v-bind:class="{'u-pagination-v1-1--active': $route.query.page == page || (!$route.query.page && page == 1)}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-19">{{ page }}</router-link>
        </li>
      </div>
      <li v-else class="list-inline-item g-hidden-sm-down">
        <span class="g-pa-12-19">...</span>
      </li>

      <li v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item">
        <router-link v-bind:to="{ path: $route.path, query: { page: curPage + 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == totalPages || totalPages == 0 }" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Next">
          <span aria-hidden="true">
            <i class="fa fa-angle-right"></i>
          </span>
          <span class="sr-only">Next</span>
        </router-link>
      </li>
      <li class="list-inline-item float-right">
        <span class="u-pagination-v1__item-info g-pa-12-19">Page {{ curPage }} of {{ totalPages }}</span>
      </li>
    </ul>
  </nav>

</template>


<script>
export default {
  name: 'Pagination',
  props: {
    curPage: {
      required: true
    },
    perPage: {
      default: 3
    },
    totalPages: {
      required: true
    },
    leftPages: {
      default: 2
    },
    rightPages: {
      default: 2
    }
  },
  computed: {
    iter_pages: function() {
      let arr = [1, 2]
      for (let i = this.leftPages; i > 0; i--) {
        arr.push(this.curPage - i)
      }
      arr.push(this.curPage)
      for (let i = 1; i <= this.rightPages; i++) {
        arr.push(this.curPage + i)
      }
      arr.push(this.totalPages - 1)
      arr.push(this.totalPages)

      arr = arr.filter(item => item > 0 && item <= this.totalPages)
      arr = [...new Set(arr)]
      if (this.curPage + this.rightPages < this.totalPages - 2) {
        arr.splice(-2, 0, 'NaN')
      }
      if (this.curPage - this.leftPages - 1 > 2) {
        arr.splice(2, 0, 'NaN')
      }
      return arr
    }
  }
}
</script>
