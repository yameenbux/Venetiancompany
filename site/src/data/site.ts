/**
 * Every client-supplied fact on the site, in one place.
 *
 * Sourced from The Venetian Company's own public Instagram (@thevenetiancompany_).
 * Nothing here is invented. If a field is not published by them it is absent,
 * not guessed — see CLAUDE.md for the do-not-invent list.
 */

export const phone = { display: '07527 180499', e164: '+447527180499' };
export const contactName = 'Adam Knowles';
export const serviceArea = 'Nationwide';

export const instagram = 'https://www.instagram.com/thevenetiancompany_/';
export const tilingPartner = 'https://www.instagram.com/sktiling/';

/** The single action the whole site pushes toward. */
export const callMessage =
  `Hi ${contactName} — I'd like to book a call about a project.\n\n` +
  `Best time to call:\nRough location:\nWhat I'm thinking:\n`;

export const whatsappCall =
  `https://wa.me/${phone.e164.replace('+', '')}?text=${encodeURIComponent(callMessage)}`;

/** Verbatim from their About Us highlight. */
export const services = [
  'Full house applications', 'Media walls', 'Bathrooms', 'Swimming pool areas',
  'Feature walls', 'Microcement', 'Staircases', 'Wet rooms', 'Floors',
] as const;

export const about = [
  `Working nationwide. The Venetian Company are a team of experienced professionals skilled in luxury Venetian plastering. We have experience creating unique and sophisticated designs to suit a variety of homes or commercial spaces.`,
  `We are a friendly, customer-focused business with a passion for bringing your dream home to reality.`,
];

/** General material fact, NOT from the client — Adam must sign this off. */
export const materials = [
  {
    name: 'Venetian plaster',
    make: 'Lime, marble dust, pigment',
    body: [
      'Built up in thin coats and burnished back as it cures. The polish comes from the tool, not a topcoat, which is why the depth sits under the surface rather than on it.',
      'Decorative before it is practical — it belongs where it will be seen and lit.',
    ],
    where: ['Walls and ceilings', 'Feature walls, media walls', 'Staircases'],
  },
  {
    name: 'Microcement',
    make: 'Cement, polymer, fine aggregate',
    body: [
      'Goes on a few millimetres thick, straight over what is already there — tile, screed, board — so floors rarely need lifting. It cures to one continuous surface with no grout lines to discolour and no joints to crack.',
      'Harder wearing, and happy with water underfoot.',
    ],
    where: ['Floors', 'Wet rooms and bathrooms', 'Swimming pool areas'],
  },
];

export const finishes = [
  { file: 'finish-venetian.jpg',    name: 'Trowelled',   alt: 'Plaster in raking light with the trowel strokes standing proud of the surface' },
  { file: 'finish-polished.jpg',    name: 'Polished',    alt: 'Polished plaster with soft cloudy movement in a pale warm grey' },
  { file: 'finish-microcement.jpg', name: 'Microcement', alt: 'Microcement laid flat and seamless in a soft warm grey' },
  { file: 'finish-textured.jpg',    name: 'Textured',    alt: 'A coarse sand-grain plaster finish' },
  { file: 'finish-pigmented.jpg',   name: 'Pigmented',   alt: 'Plaster pigmented to a soft blush, laid in broad passes', w: 390, h: 520 },
  { file: 'finish-marbled.jpg',     name: 'Marbled',     alt: 'Deep teal plaster with high-contrast marbled veining' },
];

export const work = [
  { file: 'stair-marbled.jpg',  caption: 'Feature wall — marbled',        alt: 'Deep teal marbled plaster wall behind a floating oak staircase with a glass balustrade' },
  { file: 'bathroom-blush.mp4', caption: 'Bathroom — pigmented to colour', alt: 'Pan across a bathroom finished in blush-pigmented plaster with a freestanding bath', poster: 'bathroom-blush-poster.jpg' },
  { file: 'stairwell.jpg',      caption: 'Stairwell — full height, no joins', alt: 'Double-height stairwell in polished plaster lit by a skylight above Crittall glazing' },
  { file: 'fireplace.jpg',      caption: 'Chimney breast — worked by hand', alt: 'Chimney breast in plaster with strong movement through the finish', w: 1136 },
  { file: 'texture-switch.jpg', caption: 'Detail — coarse grain',          alt: 'Coarse-grained plaster wall meeting a walnut-framed lighting keypad' },
  { file: 'plaster-detail.jpg', caption: 'Detail — the trowel, up close',  alt: 'Close detail of plaster in raking light, showing the ridges left by the trowel' },
  { file: 'wet-room.jpg',       caption: 'Wet room — microcement, no seams', alt: 'Microcement wet room with a recessed shelf and brass rainfall shower' },
  { file: 'bathroom-arch.jpg',  caption: 'Bathroom — plaster against marble', alt: 'Bathroom with a freestanding bath, arched window and plastered walls beside a marble feature wall' },
];

/** Verbatim from their Pricing, Enquiries and Deposits highlights. */
export const process = [
  { n: '01', title: 'A call first', body: `Ten minutes on the phone with ${contactName}. The space, the areas involved, and roughly what you have in mind. We can visit to see it before anything goes ahead.` },
  { n: '02', title: 'Finish, colour, samples', body: 'Once your finish, colour and other requirements are agreed, samples can be provided as part of your package — up to two included, additional samples £80.' },
  { n: '03', title: 'Quote agreed', body: 'Pricing depends on the size of the area and your desired finish. It is agreed before we commence, and we can suggest alternative finishes to suit a budget.' },
  { n: '04', title: 'Date and deposit', body: 'Once a date is mutually agreed, a 50% deposit secures the booking — it lets us buy the materials for your project, and it is non-refundable. The balance is due on completion.' },
];

export const terms = [
  'Up to 2 samples included', 'Additional samples £80',
  '50% deposit secures the booking', 'Deposit non-refundable', 'Balance due on completion',
];

/** What to have ready for the call — from their Enquiries highlight. */
export const bringToCall = [
  { req: 'Useful',      title: 'Address of the project', body: 'Where the work is.' },
  { req: 'Most useful', title: 'Photographs of the area', body: 'Wide shots beat close-ups. These are what let us price on size.' },
  { req: 'If you have them', title: 'Measurements', body: 'Rough is fine. Do not hold up the call for them.' },
  { req: 'Useful',      title: 'The finish you want', body: 'In your own words, or the inspiration photos you have been saving.' },
];
