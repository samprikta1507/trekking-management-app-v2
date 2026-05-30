<template>
  <div>
    <div>
        <div @click="$router.push('/admin')">
            Admin view 
        </div>
    </div>
    <div>
        <div @click="$router.push('/user')">
            User view
        </div>
    </div>
    <div>
        <div @click="$router.push('/staff')">
            Staff view
        </div>
    </div>

  </div>
</template> 

<script>
export default {
  name: 'LandingView',
}
</script>