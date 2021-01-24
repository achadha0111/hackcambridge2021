<template>
  <div>
    <div v-if="feedElements">

      <!-- News card -->
      <md-card v-if="currentCardType === 'P'">
        <md-card-header>
          <div class="md-title">{{feedElements[currentCard]["headline"]}}</div>
<!--          <div class="md-subhead">{{feedElements[currentCard].friends_interactions}}</div>-->
        </md-card-header>

        <md-card-content>
<!--          <a :href = feedElements[currentCard]["opinion_source"]>{{feedElements[currentCard]["opinion_source"]}}</a>-->
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
      <md-card v-if="currentCardType === 'V' || currentCardType === 'FH'">
        <md-card-header>
          <div v-if="currentCardType === 'V'"
               class="md-title">Is this video fake?</div>
          <div v-else class="md-title"> Is this a misleading headline?</div>
          <div class="md-subhead">Answer yes or no to proceed</div>
        </md-card-header>

        <md-card-media>
          <!-- Todo add video link -->
<!--          <img src="/assets/examples/avatar-2.jpg" alt="People">-->
          <youtube-media v-if="currentCardType === 'V'"
                         :video-id="feedElements[currentCard].id"></youtube-media>
        </md-card-media>

        <md-card-content>
<!--          <div v-if="currentCardType === 'fake_headline'">-->
<!--            <h2>{{feedElements[currentCard].headline}}</h2>-->
<!--          </div>-->

          <div class="rating-spectrum">
            <md-radio v-model="rating" :value=1>Fake</md-radio>
            <md-radio v-model="rating" :value=0>Not fake</md-radio>
          </div>
        </md-card-content>

        <md-card-actions>
          <md-button v-on:click="submitRating">Submit</md-button>
        </md-card-actions>
      </md-card>
      <!-- Video // Fake Headline -->

    </div>
    <div v-else>You have reached the end of your feed, check back later :)</div>
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
import axios from 'axios';

async function fetchFeedElements(callback) {
    try {
      let elements = await axios.get(`http://127.0.0.1:5000/feed`);
      callback(null, elements);
    } catch (e) {
      callback(e, null);
      console.log(e);
    }
  }

  export default {
    name: "Feed",
    data: () => ({
      feedElements: null,
      currentCardType: null,
      currentCard: 0,
      reachedEndOfFeed: false,
      rating: null,
      userInteractionEvents: [],
      error: null,
    }),

    created() {

      fetchFeedElements((err, feedElements) => {
        this.setData(err, feedElements);
      })


    },

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
          // TODO send interaction events to database
        }
      },

      setData(err, feedElements) {
        if (err) {
          this.error = err.toString;
          console.log(this.error);
        } else {
          this.feedElements = feedElements.data;
          this.currentCardType = this.feedElements[this.currentCard].CARDTYPE;
          console.log(typeof this.feedElements);
          console.log(this.feedElements[0]);
        }
      }
    }
  }
</script>