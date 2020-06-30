import tensorflow as tf
from stable_baselines.common.policies import ActorCriticPolicy

class Policy(ActorCriticPolicy):
    def __init__(
            self,
            sess,
            ob_space,
            ac_space,
            n_env,
            n_steps,
            n_batch,
            reuse=False,
            **kwargs):
        super(Policy, self).__init__(
            sess,
            ob_space,
            ac_space,
            n_env,
            n_steps,
            n_batch,
            reuse=reuse,
            scale=True)

        with tf.variable_scope("model", reuse=reuse):
            net = tf.layers.flatten(self.obs_ph)
            # print(net.shape)
            net = tf.cast(net, tf.float32)
            net = net / 2
            # Uncomment to print values of variable
            # net = tf.Print(net, [net], summarize=100)
            # TODO apply some feature processing here
            with tf.name_scope("pi_h_fc"):
                pi_h = tf.layers.dense(net, 50, activation=tf.nn.relu, name="pi_h_fc1")
                pi_h = tf.layers.dense(pi_h, 16, activation=tf.nn.relu, name="pi_h_fc2")
                pi_h = tf.layers.dense(pi_h, 2, name="pi_h_fc3")
            pi_latent = pi_h

            with tf.name_scope("vf_h_fc"):
                vf_h = tf.layers.dense(net, 50, activation=tf.nn.relu, name="vf_h_fc1")
                vf_h = tf.layers.dense(vf_h, 16, activation=tf.nn.relu, name="vf_h_fc2")
                value_fn = tf.layers.dense(vf_h, 1, name="vf_h_fc3")
                vf_latent = vf_h

            self._proba_distribution, self._policy, self.q_value = \
                self.pdtype.proba_distribution_from_latent(
                    pi_latent, vf_latent, init_scale=0.01)
        self._value_fn = value_fn
        self._setup_init()

    def step(self, obs, state=None, mask=None, deterministic=False):
        if deterministic:
            action, value, neglogp = self.sess.run([self.deterministic_action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        else:
            action, value, neglogp = self.sess.run([self.action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        return action, value, self.initial_state, neglogp

    def proba_step(self, obs, state=None, mask=None):
        return self.sess.run(self.policy_proba, {self.obs_ph: obs})

    def value(self, obs, state=None, mask=None):
        return self.sess.run(self.value_flat, {self.obs_ph: obs})
