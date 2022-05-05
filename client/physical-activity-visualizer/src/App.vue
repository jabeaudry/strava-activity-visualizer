<template>
  <div id="app">
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />
        <title>Todos</title>
    </head>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/"> Todos app </a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mx-auto">
                <li class="nav-item" :class="home_class">
                    <a class="nav-link" href="/"> Home </a>
                </li>
                <li class="nav-item" :class="add_todo_class">
                    <a class="nav-link" href="/add-todo"> Add todo </a>
                </li>
            </ul>
        </div>
    </nav>

    <router-view> </router-view>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  data() {
    return {
        home_class: this.$route.path === "/" ? "active" : "",
        add_todo_class: this.$route.path === "/add-todo" ? "active" : "",
    };
  },
}
</script>

<style>
  #app {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
