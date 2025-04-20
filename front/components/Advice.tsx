import styles from '../styles/Home.module.css'

export default function Advice() {
  return (
    <section id="safety-tips" className={styles.advice}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <img
          src="https://as2.ftcdn.net/jpg/01/03/72/93/1000_F_103729376_QE8y6FP10JyGc4kk8e2yIqrFRa921IqI.jpg"
          alt="Safety Illustration"
          style={{
            width: 350,
            height: 'auto',
            objectFit: 'contain',
            borderRadius: 16,
            marginRight: 32,
            boxShadow: '0 2px 8px rgba(24,56,43,0.10)'
          }}
        />
        <div className={styles.adviceIcon} style={{ alignSelf: 'flex-start' }}>💡</div>
        <div>
          <h2>10 Safety Tips</h2>
          <ol>
            <li><b>Keep walkways</b> clear of obstacles.</li>
            <li>Install <b>grab bars</b> in bathrooms.</li>
            <li>Ensure <b>good lighting</b> in all rooms.</li>
            <li>Use <b>non-slip mats</b> in the shower and bathtub.</li>
            <li>Wear shoes with <b>non-slip soles</b> indoors.</li>
            <li>Secure <b>loose rugs</b> with double-sided tape or remove them.</li>
            <li>Keep <b>frequently used items</b> within easy reach.</li>
            <li>Install <b>handrails</b> on both sides of stairways.</li>
            <li>Have regular <b>vision and hearing checks</b>.</li>
            <li>Consider using <b>assistive devices</b> if needed.</li>
          </ol>
        </div>
      </div>
    </section>
  )
}
