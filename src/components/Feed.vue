<template>
  <div>
    <div v-if="feedElements">

      <!-- News card -->
      <md-card v-if="currentCardType === 'news_headline'">
        <md-card-header>
          <md-avatar>
            <!-- TODO add  news outlet logo-->
<!--            <img src={{currentCard.source_logo}} alt="Avatar">-->
          </md-avatar>

          <div class="md-title">{{feedElements[currentCard].headline}}</div>
          <div class="md-subhead">{{feedElements[currentCard].friends_interactions}}</div>
        </md-card-header>

        <md-card-content>
          {{ feedElements[currentCard].news_summary}}
          <h3 class="md-subheading">Where do you think this article lies on the political spectrum?</h3>
          <div class="rating-spectrum">
            <md-radio v-model="rating" value="sLeft">Strongly Left</md-radio>
            <md-radio v-model="rating" value="Left">Left</md-radio>
            <md-radio v-model="rating" value="Centre">Centre</md-radio>
            <md-radio v-model="rating" value="Right">Right</md-radio>
            <md-radio v-model="rating" value="sRight">Strongly Right</md-radio>
          </div>
        </md-card-content>

        <md-card-actions>
          <md-button v-on:click="submitRating">Submit</md-button>
        </md-card-actions>
      </md-card>
      <!-- News card -->

      <!-- Video -->
      <md-card v-if="currentCardType === 'video' || currentCardType === 'fake_headline'">
        <md-card-header>
          <div v-if="currentCardType === 'video'"
               class="md-title">Is this video fake?</div>
          <div v-else class="md-title"> Is this a misleading headline?</div>
          <div class="md-subhead">Answer yes or no to proceed</div>
        </md-card-header>

        <md-card-media>
          <!-- Todo add video link -->
<!--          <img src="/assets/examples/avatar-2.jpg" alt="People">-->
        </md-card-media>

        <md-card-content>
          <div class="rating-spectrum">
            <md-radio v-model="rating" :value=1>Fake</md-radio>
            <md-radio v-model="rating" :value=0>Not fake</md-radio>
          </div>
        </md-card-content>

        <md-card-actions>
          <md-button v-on:click="submitRating">Submit</md-button>
        </md-card-actions>
      </md-card>
      <!-- Video -->

    </div>
  </div>
</template>

<style lang="scss" scoped>
  .md-card {
    border-radius: 4px;
    width: 320px;
    margin: 4px;
    display: inline-block;
    vertical-align: top;
}
</style>

<script>
  export default {
    name: "Feed",
    data: () => ({
      feedElements: null,
      currentCardType: null,
      currentCard: 0,
      reachedEndOfFeed: false,
      rating: null,
      userInteractionEvents: [],
    }),

    methods: {
      submitRating: () => {
        let event = {
          "user_id": "User 1",
          "item_id": this.feedElements[this.currentCard].id,
          "rating": this.rating
        }
        this.userInteractionEvents.push(event);
        let nextCard = this.currentCard + 1;

        if (nextCard !== length(this.feedElements)-1) {
          this.currentCard = nextCard;
          this.currentCardType = this.feedElements[nextCard].type;
        }

        else {
          this.reachedEndOfFeed = true;
          <!-- TODO send interaction events to database-->
        }
      }
    }
  }
</script>