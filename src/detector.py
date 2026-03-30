import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)


def get_distance(p1, p2, w, h):
    return ((p1.x * w - p2.x * w) ** 2 + (p1.y * h - p2.y * h) ** 2) ** 0.5


def analyze_frame(frame):
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_result = pose.process(rgb)
    face_result = face_mesh.process(rgb)

    score = 100
    issues = []

    # POSTURE
    if pose_result.pose_landmarks:
        lm = pose_result.pose_landmarks.landmark

        nose = lm[mp_pose.PoseLandmark.NOSE]
        l_sh = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_sh = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        nose_x, nose_y = int(nose.x * w), int(nose.y * h)
        l_sh_x, l_sh_y = int(l_sh.x * w), int(l_sh.y * h)
        r_sh_x, r_sh_y = int(r_sh.x * w), int(r_sh.y * h)

        center_x = (l_sh_x + r_sh_x) // 2
        center_y = (l_sh_y + r_sh_y) // 2

        if abs(nose_x - center_x) > 50:
            issues.append("Head Forward")
            score -= 20

        if (center_y - nose_y) < 60:
            issues.append("Slouching")
            score -= 20

        if abs(l_sh_y - r_sh_y) > 40:
            issues.append("Leaning")
            score -= 15

    # FACE
    if face_result.multi_face_landmarks:
        for face in face_result.multi_face_landmarks:
            lm = face.landmark

            eye_top = lm[159]
            eye_bottom = lm[145]
            eye_dist = get_distance(eye_top, eye_bottom, w, h)

            upper_lip = lm[13]
            lower_lip = lm[14]
            mouth_dist = get_distance(upper_lip, lower_lip, w, h)

            nose = lm[1]

            if eye_dist < 5:
                issues.append("Eyes Closed")
                score -= 30

            if mouth_dist > 20:
                issues.append("Yawning")
                score -= 15

            if nose.x < 0.3 or nose.x > 0.7:
                issues.append("Looking Away")
                score -= 20

    score = max(0, score)

    if score > 80:
        state = "FOCUSED"
    elif score > 60:
        state = "ATTENTIVE"
    elif score > 40:
        state = "LOW ATTENTION"
    elif score > 20:
        state = "DISTRACTED"
    else:
        state = "CRITICAL"

    return frame, score, state, issues